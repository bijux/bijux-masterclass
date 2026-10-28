import {
  array,
  literal,
  nullable,
  object,
  optional,
  refine,
  string,
  type Infer,
  type Schema,
} from './index.js';

const Name = refine(string(), (value) => value.trim().length > 0 && value.length <= 80, {
  code: 'project.name',
  message: 'project name must contain 1 to 80 characters',
});
const Tag = refine(string(), (value) => /^[a-z][a-z0-9-]{0,31}$/.test(value), {
  code: 'project.tag',
  message: 'tag must use lowercase letters, digits, and hyphens',
});

export const ProjectV1 = object({
  format: literal('SCHEMAKIT_PROJECT_V1'),
  name: Name,
});

export const ProjectV2 = object({
  format: literal('SCHEMAKIT_PROJECT_V2'),
  name: Name,
  tags: array(Tag, { maxLength: 32 }),
  owner: optional(object({
    name: Name,
    email: optional(nullable(string())),
  })),
});

export type ProjectV1 = Infer<typeof ProjectV1>;
export type ProjectV2 = Infer<typeof ProjectV2>;

export const Project: Schema<ProjectV1 | ProjectV2> = {
  kind: 'project',
  safeParse(input: unknown) {
    const v2 = ProjectV2.safeParse(input);
    if (v2.ok) return v2;
    return ProjectV1.safeParse(input);
  },
  parse(input: unknown) {
    const result = this.safeParse(input);
    if (result.ok) return result.value;
    return ProjectV2.parse(input);
  },
};

export function migrateProject(project: ProjectV1 | ProjectV2): ProjectV2 {
  if (project.format === 'SCHEMAKIT_PROJECT_V2') return project;
  return Object.freeze({ format: 'SCHEMAKIT_PROJECT_V2', name: project.name, tags: Object.freeze([]) });
}
