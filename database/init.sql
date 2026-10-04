CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL
);

INSERT INTO projects (name, description)
VALUES
('AWS Migration', 'Migration of workloads to AWS'),
('CI/CD Automation', 'Jenkins based CI/CD pipeline'),
('Docker Deployment', 'Containerized application deployment');
