import pg, {
  type Pool as PgPool,
  type PoolClient,
  type QueryResultRow,
} from "pg";

const { Pool } = pg;

export type Row = QueryResultRow & Record<string, any>;

/**
 * Owns the PostgreSQL pool and the transaction protocol used by the course.
 *
 * Callers receive one checked-out client for the complete transaction. A
 * callback may not retain the client after the promise settles.
 */
export class Database {
  public readonly pool: PgPool;

  public constructor(url: string) {
    this.pool = new Pool({
      connectionString: url,
      max: 16,
      connectionTimeoutMillis: 5_000,
      idleTimeoutMillis: 30_000,
    });
  }

  public async transaction<T>(
    work: (client: PoolClient) => Promise<T>,
  ): Promise<T> {
    const client = await this.pool.connect();
    try {
      await client.query("BEGIN");
      const value = await work(client);
      await client.query("COMMIT");
      return value;
    } catch (error) {
      try {
        await client.query("ROLLBACK");
      } catch (rollbackError) {
        (error as Error & { cause?: unknown }).cause ??= rollbackError;
      }
      throw error;
    } finally {
      client.release();
    }
  }

  public async health(): Promise<void> {
    await this.pool.query("SELECT 1");
  }

  public async close(): Promise<void> {
    await this.pool.end();
  }
}
