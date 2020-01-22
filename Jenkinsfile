pipeline {
    agent { docker { image 'python:3.6.8' } }
    environment {
        ENV_VAR      = 'dummy'
    }
    stages {
        stage('Build'){
            steps {
                sh 'python --version'
		sh 'git fetch'
                script {
                    diff_files = sh (script:'git diff --name-only origin/master | xargs',
                                     returnStdout: true).trim()
                    for (int i = 0; i < diff_files.size(); i++) {
                        echo "${diff_files[i]}"
                    } 
                }
            }
        }
        stage('Test') {
            steps { 
                sh 'ls' 
            }
        }
    }
}
