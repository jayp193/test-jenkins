pipeline {
    agent any
    stages {
        stage('Build'){
            steps {
		sh 'git fetch'
                diff_files = sh 'git diff --name-only origin/master | xargs' 
            }
        }
        stage('Test') {
            steps { 
                sh 'ls' 
            }
        }
    }
}
