pipeline {
    agent any

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
                sh """
                    export DOCKER_BUILDKIT=1
                    docker build -t ${FULL_IMAGE} .
                """
            }
        }

        stage('Lint (inside Docker)') {
            steps {
                sh """
                    docker run --rm ${FULL_IMAGE} bash -c ' flake8 . && black . '
                """
            }
        }

        stage('Tests (inside Docker)') {
            steps {
                sh """
                    docker run --rm ${FULL_IMAGE} python3 -m pytest \
                    --disable-warnings --maxfail=1 \
                    --cov=app --cov-report=xml:coverage.xml
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
