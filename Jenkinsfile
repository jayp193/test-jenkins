pipeline { 
    agent any
    environment {
        PROJECTS_AVAIL = "streaming-api-client;rest-api-python-scripts"
        TEST_RESULTS = ""
    }
    stages {
        stage('Build'){
            steps {   
                sh 'python --version'
                sh 'git fetch'
                script {
                    commitChangeset = sh(returnStdout: true, script: 'git diff-tree --no-commit-id --name-status -r HEAD').trim()
                    proj = env.PROJECTS_AVAIL.tokenize(';')
                    println(proj)
                    println(proj.size())
                    tests = []
                    for (int i = 0; i < proj.size(); i++) {
                        if (commitChangeset.contains(proj[i])) {
                            tests.add(proj[i])
                        }
                    }
                    env.TESTS_TO_RUN = tests.join(';')
                } 
            }
        }
        stage('Test') {
            steps {   
                sh 'ls'
                echo "${TESTS_TO_RUN}"
            }
        }
    }
}
