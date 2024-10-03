import React from 'react';
import styles from './DashboardStyles.module.css';
import ScoreCard from '../../common/SecurityScoreCard';
import NetworkTrafficCard from '../../common/NetworkTrafficCard';
import RealTimeThreatsCard from '../../common/RealTimeThreatsCard';
import OpenPortsCard from '../../common/OpenPortsCard';
import VulnerabilityOverviewCard from '../../common/VunerabilityOverviewCard';
import SslDnsStatusCard from '../../common/SslDnsStatusCard';
import risk from '../../assets/risk.png';
//each import represents a component that will pull information from another process
//and display a quick look into that diagnostic

function Dashboard() {
    //This return contains the contents of the home dashboard page, 
    //from here, we can easily remove and add components and information
    //that we want to display. Hoping to add graphs once the exact data is
    //configured to displat here
      return (
        <section id="dashboard" className={styles.container}>
            <h1 className={styles.sectionTitle}>Dashboard Prototype</h1>
            <div className={styles.cardsContainer}>
                <ScoreCard 
                    src={risk} 
                    link="https://github.com/" 
                    h3="Threat Score"
                    p="735"
                />
                <NetworkTrafficCard
                    link="https://github.com/" 
                    h3="Network Traffic"
                />
                <RealTimeThreatsCard
                    link="https://github.com/" 
                    h3="Real Time Threats"
                />
                <OpenPortsCard
                    link="https://github.com/" 
                    h3="Open Ports"
                />
                <VulnerabilityOverviewCard
                    link="https://github.com/" 
                    h3="Vulnerability Overview"
                />
                <SslDnsStatusCard
                    link="https://github.com/" 
                    h3="SSL and DNS Status"
                />
            </div>
        </section>
    );
  }
  
  export default Dashboard;