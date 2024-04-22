# JobAssistant
🔍 Job searching automated with AI | 🎯 Apply to jobs is simplified


---
# Get Started

# replace branchName by branch you want to clone (e.g: main)
git clone -b branchName https://your_pseudo:token@github.com/Zapony/JobAssistant

pip install -r backend/requirements.txt

#Grant execution permissions and start servers

chmod +x start_servers.sh
sudo ./start_servers.sh


### Stopping the Backend Server:
To stop the backend server running on port 9000, execute the following command:

```bash
sudo kill $(sudo lsof -t -i:9000)
```