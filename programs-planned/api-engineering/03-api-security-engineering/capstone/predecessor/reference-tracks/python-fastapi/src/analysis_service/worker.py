"""Durable job and webhook-delivery worker."""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import logging
from pathlib import Path
import signal
import threading

from .artifacts import FileSystemArtifactStore
from .config import Settings
from .domain import canonical_json, webhook_signature
from .failures import LeaseLost
from .ports import ClaimedJob, OutboundTransport, Repository
from .postgres import PostgresRepository
from .remote_fixtures import RemoteFixtureError, resolve_remote_fixture
from .webhooks import HttpxOutboundTransport


LOG = logging.getLogger("analysis-worker")
READ_CHUNK_SIZE = 64 * 1024


class PermanentJobFailure(RuntimeError):
    """A failure that retrying the same durable input cannot repair."""


class Worker:
    def __init__(
        self,
        repository: Repository,
        store: FileSystemArtifactStore,
        transport: OutboundTransport,
        settings: Settings,
    ) -> None:
        self.repository = repository
        self.store = store
        self.transport = transport
        self.settings = settings
        self.stop = threading.Event()

    def _source_path(self, job: ClaimedJob) -> Path:
        if job.source_kind == "local-file":
            if not job.content_path:
                raise PermanentJobFailure(
                    "ready local dataset has no content path"
                )
            return self.store.path_for(
                job.content_path,
                job.expected_checksum,
            )

        return resolve_remote_fixture(
            self.settings.remote_fixture_root,
            str(job.source.get("uri", "")),
        )

    def _analyze(self, job: ClaimedJob) -> dict[str, object]:
        digest = sha256()
        size = 0
        lines = 0
        last_byte = b""
        chunks = 0

        with self._source_path(job).open("rb") as stream:
            while block := stream.read(READ_CHUNK_SIZE):
                digest.update(block)
                size += len(block)
                lines += block.count(b"\n")
                last_byte = block[-1:]
                chunks += 1
                if chunks % 8 == 0:
                    self.repository.renew_job_lease(
                        job,
                        self.settings.worker_lease_seconds,
                    )

        if size and last_byte != b"\n":
            lines += 1

        actual_checksum = digest.hexdigest()
        expected_checksum = job.expected_checksum or job.source.get(
            "checksumSha256"
        )
        if expected_checksum and actual_checksum != expected_checksum:
            raise PermanentJobFailure(
                "dataset checksum does not match the durable contract"
            )

        common: dict[str, object] = {
            "algorithm": job.algorithm,
            "bytes": size,
            "sha256": actual_checksum,
        }
        if job.algorithm == "line-count":
            return {**common, "lines": lines}
        if job.algorithm == "checksum":
            return common
        return {**common, "lines": lines, "nonEmpty": size > 0}

    def process_one_job(self) -> bool:
        job = self.repository.claim_job(
            self.settings.worker_id,
            self.settings.worker_lease_seconds,
        )
        if job is None:
            return False

        try:
            self.repository.mark_job_running(job)
            result = self._analyze(job)
            self.repository.renew_job_lease(
                job,
                self.settings.worker_lease_seconds,
            )

            # Both language tracks publish these exact bytes—no trailing newline.
            payload = canonical_json(result)
            staged = self.store.stage_bytes(payload, "application/json")
            key = (
                f"artifacts/{staged.checksum_sha256[:2]}/"
                f"{staged.checksum_sha256}"
            )
            self.store.publish(staged, key)
            self.repository.complete_job(
                job,
                staged,
                key,
                f"{job.algorithm}.json",
                {
                    "algorithm": job.algorithm,
                    "artifactCount": 1,
                },
            )
            return True
        except LeaseLost:
            LOG.warning(
                "lease lost; stale worker result ignored",
                extra={
                    "run_id": job.run_id,
                    "generation": job.lease_generation,
                },
            )
            return True
        except (PermanentJobFailure, RemoteFixtureError) as exc:
            LOG.warning(
                "job failed permanently",
                extra={"run_id": job.run_id, "reason": str(exc)},
            )
            self._report_failure(job, exc, retryable=False)
            return True
        except Exception as exc:  # infrastructure failures are retry candidates
            LOG.exception(
                "job failed",
                extra={"run_id": job.run_id, "attempt": job.attempt},
            )
            self._report_failure(job, exc, retryable=True)
            return True

    def _report_failure(
        self,
        job: ClaimedJob,
        error: Exception,
        *,
        retryable: bool,
    ) -> None:
        try:
            self.repository.fail_job(
                job,
                "worker-error",
                str(error),
                retryable,
            )
        except LeaseLost:
            LOG.warning(
                "failure report ignored after lease loss",
                extra={"run_id": job.run_id},
            )

    def process_one_delivery(self) -> bool:
        self.repository.expand_outbox()
        delivery = self.repository.claim_delivery(
            self.settings.worker_id,
            self.settings.worker_lease_seconds,
        )
        if delivery is None:
            return False

        body = canonical_json(delivery.payload)
        timestamp = str(int(datetime.now(timezone.utc).timestamp()))
        headers = {
            "Content-Type": "application/json",
            "X-Event-Id": delivery.event_id,
            "X-Webhook-Timestamp": timestamp,
            "X-Webhook-Signature": webhook_signature(
                delivery.secret,
                timestamp,
                body,
            ),
        }
        try:
            status = self.transport.post(
                delivery.target_url,
                body,
                headers,
                3.0,
            )
            if 200 <= status < 300:
                self.repository.record_delivery_success(delivery, status)
            else:
                retryable = status >= 500 or status in {408, 425, 429}
                self.repository.record_delivery_failure(
                    delivery,
                    f"receiver returned {status}",
                    retryable,
                )
        except LeaseLost:
            LOG.warning(
                "delivery lease lost",
                extra={"event_id": delivery.event_id},
            )
        except Exception as exc:
            try:
                self.repository.record_delivery_failure(
                    delivery,
                    str(exc),
                    True,
                )
            except LeaseLost:
                LOG.warning(
                    "delivery failure ignored after lease loss",
                    extra={"event_id": delivery.event_id},
                )
        return True

    def run(self) -> None:
        try:
            while not self.stop.is_set():
                self.repository.recover_expired_jobs()
                self.repository.recover_expired_deliveries()

                # Evaluate both paths every cycle.  A busy job queue must not
                # starve webhook delivery, and vice versa.
                processed_job = self.process_one_job()
                processed_delivery = self.process_one_delivery()
                if not processed_job and not processed_delivery:
                    self.stop.wait(0.25)
        finally:
            close = getattr(self.repository, "close", None)
            if close:
                close()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    settings = Settings.from_env()
    repository = PostgresRepository(
        settings.database_url,
        settings.webhook_encryption_key,
        settings.callback_signing_secret,
        settings.service_release,
    )
    repository.open()
    worker = Worker(
        repository,
        FileSystemArtifactStore(settings.artifact_root),
        HttpxOutboundTransport(settings.webhook_transport_base),
        settings,
    )
    signal.signal(signal.SIGTERM, lambda *_: worker.stop.set())
    signal.signal(signal.SIGINT, lambda *_: worker.stop.set())
    worker.run()


if __name__ == "__main__":
    main()
