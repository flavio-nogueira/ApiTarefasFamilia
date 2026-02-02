pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE = 'flavionogueira/api-tarefas-familia'
        DOCKER_TAG = "${BUILD_NUMBER}"
        SONAR_HOST = 'http://localhost:9000'
        KUBECONFIG = credentials('kubeconfig-k8s')
        K8S_NAMESPACE = 'api-tarefas'
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
            environment {
                SONAR_TOKEN = credentials('sonar-token')
            }
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=api-tarefas-familia \
                            -Dsonar.sources=api_tarefas_familia \
                            -Dsonar.host.url=${SONAR_HOST} \
                            -Dsonar.login=${SONAR_TOKEN}
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh """
                            echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin
                            docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                            docker push ${DOCKER_IMAGE}:latest
                        """
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh """
                        export KUBECONFIG=${KUBECONFIG}

                        # Criar namespace se nao existir
                        kubectl create namespace ${K8S_NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

                        # Aplicar configuracoes
                        kubectl apply -f k8s/configmap.yaml -n ${K8S_NAMESPACE}
                        kubectl apply -f k8s/secret.yaml -n ${K8S_NAMESPACE}
                        kubectl apply -f k8s/deployment.yaml -n ${K8S_NAMESPACE}
                        kubectl apply -f k8s/service.yaml -n ${K8S_NAMESPACE}

                        # Atualizar imagem do deployment
                        kubectl set image deployment/api-tarefas-familia \
                            api-tarefas-familia=${DOCKER_IMAGE}:${DOCKER_TAG} \
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
                        export KUBECONFIG=${KUBECONFIG}

                        # Obter IP do servico
                        SERVICE_IP=\$(kubectl get svc api-tarefas-familia -n ${K8S_NAMESPACE} -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

                        if [ -z "\$SERVICE_IP" ]; then
                            SERVICE_IP=\$(kubectl get svc api-tarefas-familia -n ${K8S_NAMESPACE} -o jsonpath='{.spec.clusterIP}')
                        fi

                        echo "Service IP: \$SERVICE_IP"

                        # Testar health endpoint
                        for i in 1 2 3 4 5; do
                            if curl -s -f "http://\$SERVICE_IP:8000/health" > /dev/null; then
                                echo "Health check passed!"
                                exit 0
                            fi
                            echo "Attempt \$i failed, retrying..."
                            sleep 10
                        done

                        echo "Health check failed!"
                        exit 1
                    """
                }
            }
        }
    }

    post {
        always {
            cleanWs()
            sh 'docker system prune -f || true'
        }
        success {
            echo 'Pipeline executado com sucesso!'
        }
        failure {
            echo 'Pipeline falhou!'
        }
    }
}
