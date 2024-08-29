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
  - name: custom-agent
    image: bitnami/kubectl:latest
    command:
      - "/bin/sh"
      - "-c"
      - |
        apk add --no-cache python3 py3-pip && \
        pip3 install pytest && \
        sleep 99d
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
                    deployToKubernetes('k8s/deployment.yaml', 'k8s/service.yaml', 'fastapi-app-service', '80' , '8000')
                }
            }
        }
    }
}
