#!/usr/bin/groovy

pipeline {
    agent none

    options {
        disableConcurrentBuilds()
    }

    environment {
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_PROJECT_KEY = 'restmon-sonar-project'
        IMAGE_NAME = 'restmon'
        TAG = 'latest'
    }

    stages {
        stage('Build Docker image') {
            agent { label 'master1' }
            steps {
                sh """
                     export DOCKER_BUILDKIT=1
                     docker build -t ${IMAGE_NAME}:${TAG} .
                """
            }
        }

        stage('Lint (inside Docker)') {
            agent { label 'master2' }
            steps {
                sh("docker run --rm ${IMAGE_NAME}:${TAG} bash -c ' black . && flake8 . --ignore=E501'")
            }
        }

        stage('Run Unit Tests') {
            agent { label 'master3' }
            steps {
                sh """
                    docker run --rm \
                    ${IMAGE_NAME}:${TAG} \
                    python3 -m pytest -v --cov=restmon --cov-report=xml:coverage/coverage.xml tests
                """
            }
        }

        stage('Integration Tests') {
            agent { label 'master4' }
            steps {
                sh """
                    docker run --rm \
                    ${IMAGE_NAME}:${TAG} \
                    ./run_int_test.sh
                """
            }
        }

        stage('SonarQube Analysis') {
            agent { label 'master5' }
            steps {
                withSonarQubeEnv('SonarQube') {
                        sh """
                            ${tool('SonarScanner')}/bin/sonar-scanner \
                                -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                                -Dsonar.sources=restmon \
                                -Dsonar.python.coverage.reportPaths=coverage/сoverage.xml \
                                -Dsonar.scanner.skipJreProvisioning=true \
                                -Dsonar.scanner.caches.directory=.sonar/cache
                        """
                }
            }
        }

        /*stage('Quality Gate') {
            steps {
                timeout(time: 30, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }*/
    }

    post {
        always {
            echo 'Pipeline finished.'
            cleanWs() // Clean workspace after build
        }
    }
}
