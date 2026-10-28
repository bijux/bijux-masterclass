import assert from 'node:assert/strict';
import test from 'node:test';
import { migrateProject, Project, ProjectV1, ProjectV2 } from '../src/project.js';

test('project versions validate and V1 migrates canonically', () => {
  const old = ProjectV1.parse({ format: 'SCHEMAKIT_PROJECT_V1', name: 'Legacy' });
  assert.deepEqual({ ...migrateProject(old) }, { format: 'SCHEMAKIT_PROJECT_V2', name: 'Legacy', tags: [] });
  assert.equal(ProjectV2.safeParse({ format: 'SCHEMAKIT_PROJECT_V2', name: 'Current', tags: ['typescript'] }).ok, true);
  assert.equal(Project.safeParse({ format: 'UNKNOWN', name: 'x' }).ok, false);
});
