pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'localhost:32000'
        DOCKER_IMAGE = 'api-tarefas-familia'
        DOCKER_TAG = "${BUILD_NUMBER}"
        K8S_NAMESPACE = 'api-tarefas'
        SONAR_HOST = 'http://76.13.69.127:9000'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Branch: ${env.GIT_BRANCH}"
                echo "Commit: ${env.GIT_COMMIT}"
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            sonar-scanner \
                            -Dsonar.projectKey=api-tarefas-familia \
                            -Dsonar.projectName='API Tarefas Familia' \
                            -Dsonar.sources=api_tarefas_familia \
                            -Dsonar.host.url=${SONAR_HOST}
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh """
                        docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh """
                        # Criar namespace se nao existir
                        kubectl create namespace ${K8S_NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

                        # Aplicar configuracoes
                        kubectl apply -f k8s/configmap.yaml -n ${K8S_NAMESPACE}
                        kubectl apply -f k8s/secret.yaml -n ${K8S_NAMESPACE}
                        kubectl apply -f k8s/deployment.yaml -n ${K8S_NAMESPACE}
                        kubectl apply -f k8s/service.yaml -n ${K8S_NAMESPACE}
                        kubectl apply -f k8s/ingress.yaml -n ${K8S_NAMESPACE}

                        # Atualizar imagem do deployment
                        kubectl set image deployment/api-tarefas-familia \
                            api-tarefas-familia=${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG} \
                            -n ${K8S_NAMESPACE}

                        # Aguardar rollout
                        kubectl rollout status deployment/api-tarefas-familia -n ${K8S_NAMESPACE} --timeout=300s
                    """
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    sh """
                        echo "API URL: http://76.13.69.127/apitarefasfamilia"
                        echo "Swagger: http://76.13.69.127/apitarefasfamilia/swagger"

                        # Testar health endpoint via Ingress
                        for i in 1 2 3 4 5; do
                            if curl -s -f "http://76.13.69.127/apitarefasfamilia/health" > /dev/null 2>&1; then
                                echo "Health check passed!"
                                exit 0
                            fi
                            echo "Attempt \$i failed, retrying..."
                            sleep 10
                        done

                        echo "Health check failed - verificar logs do pod"
                        kubectl logs -l app=api-tarefas-familia -n ${K8S_NAMESPACE} --tail=50
                        exit 1
                    """
                }
            }
        }
    }

    post {
        always {
            sh 'docker system prune -f || true'
        }
        success {
            echo '========================================='
            echo 'Pipeline executado com sucesso!'
            echo 'API: http://76.13.69.127/apitarefasfamilia'
            echo 'Swagger: http://76.13.69.127/apitarefasfamilia/swagger'
            echo '========================================='
        }
        failure {
            echo 'Pipeline falhou!'
        }
    }
}
