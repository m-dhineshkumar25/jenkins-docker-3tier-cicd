pipeline {
    agent any

    stages {

        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Build") {
            steps {
                sh "docker compose build"
            }
        }

        stage("Deploy") {
            steps {
                sh """
                    cp .env.example .env
                    docker compose up -d
                """
            }
        }

        stage("Health Check") {
            steps {
                sh """
                    sleep 15
                    curl -f http://localhost/api/health
                    docker compose ps
                """
            }
        }

        stage("Cleanup") {
            steps {
                sh "docker image prune -f"
            }
        }
    }

    post {
        success {
            echo "CI/CD deployment completed successfully."
        }

        failure {
            echo "CI/CD pipeline failed."
        }
    }
}
