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
    }

    stages {
        stage('Build Docker image') {
            steps {
                buildApp()
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

        stage('Run Unit Tests') {
            steps {
                runUnitTests()
            }
            post {
                always {
                    afterTests()
                }
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

buildApp {
    sh """
        export DOCKER_BUILDKIT=1
        docker build -t ${FULL_IMAGE} .
        docker run -d --name app api
        docker ps -a
    """
}

runUnitTests {
    sh('docker exec app python3 -m unittest discover')
}

afterTests {
    sh('docker rm -f app')
}
