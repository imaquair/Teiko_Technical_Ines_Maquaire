# Teiko_Technical_Ines_Maquaire

## Part 1: Data Management

The data is stored in a **SQLite relational database** using three related tables:

- **Projects** — Stores each unique project.
- **Subjects** — Stores patient-level information, including condition, age, sex, treatment, and response. Each subject belongs to a project.
- **Samples** — Stores individual biological samples, including sample type, time from treatment start, and the five immune cell counts. Each sample belongs to a subject.

The database follows the following relationship: `Project → Subject → Sample`

This structure avoids repeating patient and project information across samples and makes the database easier to query and scale.

### Running the Data Loader

From the repository root, run:

```bash
python load_data.py