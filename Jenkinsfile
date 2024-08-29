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
            label "shell"
            defaultContainer "shell"
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: kubectl
    image: bitnami/kubectl:latest
    command:
      - "/bin/sh"
      - "-c"
      - "sleep 99d"
    tty: true
    securityContext:
      runAsUser: 0
  - name: dind
    image: docker:27.1.2
    command: ['cat']
    tty: true
    resources:
        limits:
            memory: "2Gi"
            cpu: "1000m"
        requests:
            memory: "500Mi"
            cpu: "500m"
    volumeMounts:
    - name: dockersock
      mountPath: /var/run/docker.sock
  volumes:
  - name: dockersock
    hostPath:
      path: /var/run/docker.sock
"""
        }
    }
    environment {
       
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials') // Docker Hub credentials in Jenkins
        DOCKER_IMAGE = "fastapi-app:latest"
        DOCKERHUB_REPO = "selmaguedidi/fastapi-app"
    }
    stages {
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
                container('kubectl') {
                    deployToKubernetes('k8s/deployment.yaml', 'k8s/service.yaml', fastapi-app-service, '80' , '8000')
                }
            }
        }
    }
}
