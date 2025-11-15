pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-monitoring:latest'
        DOCKER_NETWORK = 'devops-net'
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_PROJECT_KEY = 'flask-monitoring'
        PATH = "/opt/sonar-scanner/bin:${PATH}"
        PIP_CACHE_VOLUME = 'pip-cache'
    }

    stages {

        stage('Build') {
            steps {
                echo 'Building Docker image with BuildKit and pip cache...'
                sh """
                    docker build --build-arg PIP_CACHE_DIR=/root/.cache/pip \
                        -t $DOCKER_IMAGE .
                """
            }
        }

        stage('Lint') {
            steps {
                echo 'Running flake8 and black check...'
                sh '''
                docker run --rm --network $DOCKER_NETWORK $DOCKER_IMAGE \
                    bash -c "flake8 app && black --check app"
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running pytest with coverage...'
                sh '''
                docker run --rm --network $DOCKER_NETWORK $DOCKER_IMAGE \
                    -v "$PWD":/app \
                    -v pytest-cache:/app/.pytest_cache \
                    python3 -m pytest --disable-warnings --maxfail=1 \
                    --cov=app --cov-report=xml:coverage.xml /app/tests
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    script {
                        def scannerHome = tool 'SonarScanner'
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                                -Dsonar.sources=app \
                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                -Dsonar.scanner.skipJreProvisioning=true \
                                -Dsonar.scanner.caches.directory=.sonar/cache
                        """
                    }
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
