import React from 'react';

function RealTimeThreatsCard({link, h3 }) {
    const alerts = [ /*An array that we can transform to import from transformed log files*/
        'Malware detected in network (IP: 192.168.1.50)',
        'Suspicious login from unknown device',
        'Phishing attempt blocked on domain: example.com'
      ];
  return (
    <a href={link} target="_blank">
        <h3>{h3}</h3>
        <ul>
            {alerts.map((alert, index) => (<li key={index}>{alert}</li>))}
        </ul>
    </a>
  );
};

export default RealTimeThreatsCard;