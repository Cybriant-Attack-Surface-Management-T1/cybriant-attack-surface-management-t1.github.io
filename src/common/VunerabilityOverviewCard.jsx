import React from 'react';

function VunerabilityOverviewCard({link, h3 }) {/*This will be transformed to take arguemnts*/
  return (                                      /*from other processes*/
    <a >
        <h3>{h3}</h3>
        <p><strong>Security Health:</strong> Moderate</p>   
        <ul>
        <   li>3 Critical Vulnerabilities</li>
            <li>5 Medium Vulnerabilities</li>
            <li>12 Low Vulnerabilities</li>
        </ul>
    </a>
  );
};

export default VunerabilityOverviewCard;