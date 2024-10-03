import React from 'react';

function RealTimeThreatsCard({link, h3 }) {
    const openPorts = [ /*An array that we can transform to import from transformed log files*/
        'Port 22 (SSH)',
        'Port 80 (HTTP)',
        'Port 443 (HTTPS)',
        'Port 3389 (RDP)',
        'Port 3306 (MySQL)'
      ];
  return (
    <a href={link} target="_blank">
        <h3>{h3}</h3>
        <ul>
            {openPorts.map((port, index) => (<li key={index}>{port}</li>))}
        </ul>
    </a>
  );
};

export default RealTimeThreatsCard;