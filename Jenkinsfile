pipeline {
    agent any
    environment {
        ENV_VAR      = 'dummy'
    }
    stages {
        stage('Build'){
            steps {
                sh 'python --version'
	        sh 'git fetch'
                script {
                    println("Try1: ")
                    commitChangeset = sh(returnStdout: true, script: 'git diff-tree --no-commit-id --name-status -r HEAD').trim()
                    println("ChangeSets are:")
                    println(commitChangeset)
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

