#!/usr/bin/groovy

pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_PROJECT_KEY = 'flask-monitoring'
        REGISTRY = 'justtheloka.com'
        IMAGE = 'flask-monitoring-production'
        TAG = 'latest'
        FULL_IMAGE = "${REGISTRY}/${IMAGE}:${TAG}"
        TEST_APP = 'restmon_test'
    }

    stages {
        stage('Build Docker image') {
            steps {
                sh """
                     export DOCKER_BUILDKIT=1
                     docker build -t ${FULL_IMAGE} .
                """
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh """
                    docker run -d --name ${TEST_APP} ${FULL_IMAGE}
                    docker ps -a
                    docker exec ${TEST_APP} python3 -m unittest discover
                """
            }
            post {
                always {
                    sh('docker rm -f app')
                }
            }
        }

        stage('Lint (inside Docker)') {
            steps {
                sh("docker run --rm ${FULL_IMAGE} bash -c ' black . && flake8 . '")
            }
        }

        stage('Coverage Tests') {
            steps {
                sh """
                    docker run --rm ${FULL_IMAGE} \
                    python3 -m pytest \
                    --disable-warnings --maxfail=1 \
                    --cov=. --cov-report=xml:coverage.xml
                """
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                        sh """
                            ${tool('SonarScanner')}/bin/sonar-scanner \
                                -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                                -Dsonar.sources=. \
                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                -Dsonar.scanner.skipJreProvisioning=true \
                                -Dsonar.scanner.caches.directory=.sonar/cache
                        """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 30, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
            cleanWs() // Clean workspace after build
        }
    }
}
