<h1 align="center">
  <br> 
  <a ><img src="https://i.imgur.com/uv8dr81.gif[/img]"
  <br>
  
  Discord-Image-Converter
  <br>
</h1>

<h4 align="center">Fast Image Conversion, No Coding Skills Required.</h4>

<p align="center">
  <a href="#overview">Overview</a>
  •
  <a href="#installation">Installation</a>
  •
  <a href="https://github.com/luh-99/Discord-Image-Converter/blob/a07e97f85b2b313945aa1279f885f6dc226c0b52/LICENSE">License</a>
</p>

# Installation

Deploying on Railway
Sign up / login to [Railway](railway.app)
Fork this repository
Create a new project on Railway: select "Deploy from GitHub repo" and connect the forked repository.
After deployment starts, go to "Variables" tab.
Add a variable:
|      KEY      |        VALUE        |
| DISCORD_TOKEN | your_bot_token_here |

Trigger a redeploy if needed to pick the env variables.
Your bot should come online and work!
Additional tips:
On Railway free tier, your bot might sleep after inactivity, that's fine for testing.
Consider upgrading or use other platforms for guaranteed uptime.
Use Railway logs to debug any issues.
For large video conversions, be mindful of memory/CPU usage limits.
Alternative: Deploy on Heroku (similar steps)
Create a Heroku app.
Push your code.
Set environment variable DISCORD_TOKEN with your bot token.
Set Procfile same way.
Heroku will keep bot running (free dyno sleeps after inactivity, can upgrade).
