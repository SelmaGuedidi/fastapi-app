@Library('my-shared-library@main') _
properties([
    pipelineTriggers([
        githubPush()
    ])
])

pipeline {
    agent {
        kubernetes {
            cloud "minikube"
            yamlFile "pod-template.yaml"
        }
    }
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials') // Docker Hub credentials in Jenkins
        DOCKER_IMAGE = "fastapi-app:latest"
        DOCKERHUB_REPO = "selmaguedidi/fastapi-app"
    }
    stages {
        stage('Run unit tests') {
            steps {
                container('custom-agent') {
                    sh 'pytest'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                container('dind') {
                    buildDockerImage(DOCKER_IMAGE)
                }
            }
        }
        stage('Tag and Push Docker Image') {
            steps {
                container('dind') {
                    pushDockerImage(DOCKER_IMAGE, DOCKERHUB_REPO)
                }
            }
        }
        stage('Deploy to Minikube') {
            steps {
                container('custom-agent') {
                    deployToKubernetes('k8s/deployment.yaml', 'k8s/service.yaml', 'fastapi-app-service', '80', '8000')
                }
            }
        }
    }
}
