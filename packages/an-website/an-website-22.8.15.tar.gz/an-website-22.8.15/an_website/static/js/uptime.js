// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt GNU-AGPL-3.0-or-later
"use strict";function startDisplayingUptime(){const uptimeDiv=elById("uptime");uptimeDiv.style.fontFamily="'clock-face', monospace";const startTime=(performance.now()/1000)-parseFloat(uptimeDiv.getAttribute("uptime"));const zeroPad=n=>String(Math.floor(n)).padStart(2,"0");const displayUptime=()=>{const uptime=Math.floor((performance.now()/1000)-startTime);const div_60=Math.floor(uptime/60);const div_60_60=Math.floor(div_60/60);uptimeDiv.innerText=[zeroPad(div_60_60/24),zeroPad(div_60_60%24),zeroPad(div_60%60),zeroPad(uptime%60)].join(":");uptimeDiv.setAttribute("uptime",String(uptime));};displayUptime();setInterval(displayUptime,1000);}
startDisplayingUptime();
// @license-end
