import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';  // Automatically registers all chart components
import '../pages/CSS/Trackrecord.css';
import axios from 'axios';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale } from 'chart.js';

// Register required components
ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale);

function Trackrecord() {
  const [chartData, setChartData] = useState(null);
  const [eventRecord, setEventRecord] = useState(null)

  useEffect(() => {
    axios.get('https://ufc-picks-api-5897a84a5ddf.herokuapp.com/get-trackrecord')
        .then(response => {
            const data = response.data;
            const labels = data.map(item => item.Event);
            const chartData = data.map(item => item.Cumulative_Units);

            const ufcChart = {
                labels: labels,
                datasets: [{
                    label: 'Cumulative Units',
                    data: chartData,
                    borderColor: '#FFD700',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    fill: false,
                    tension: 0.1
                }]
            };
            setChartData(ufcChart);
        })
        .catch(error => {
            console.error('Error fetching the track record:', error);
        });
  }, []);

  const handleChartClick = async (event, elements) => {
    if (elements.length > 0) {
      const index = elements[0].index;
      const eventLabel = chartData.labels[index];

      try {
        const response = await axios.get(`https://ufc-picks-api-5897a84a5ddf.herokuapp.com/get-event-trackrecord?event=${encodeURIComponent(eventLabel)}`);
        console.log(response.data)
        setEventRecord(response.data);
      } catch (error) {
        console.error('Error fetching event details:', error);
      }
    }
  };
  
  return (
    <>
    <div className='Trackrecord-container'>
      <h1>UFC Model Performance</h1>
      <div className="chart-container">
      {chartData && <Line data={chartData} options={{
        maintainAspectRatio: false,
          scales: {
            x: {
              title: {
                display: true,
                text: 'Event',
                font:{
                    family: "BebasNeue",
                    size: 16
                }
              },
              ticks: {
                maxRotation: 45, // Rotate labels to 45 degrees
                minRotation: 45,
                font: {
                  family: 'BebasNeue'
                }
              }
            },
            y: {
              title: {
                display: true,
                text: 'Cumulative Units',
                font:{
                  family: "BebasNeue",
                    size: 16
                }
              },
              min: -5,
              max: 1
            }
          },           
          plugins: {
            legend: {
              display: false
            }
          },
          onClick: (event, elements) => handleChartClick(event, elements)
        }} />}
        </div>
        <div className='Trackrecord-individual-container'>
            {eventRecord && (
                <div>
                    <h2>{eventRecord.event}</h2>
                    <p>{eventRecord.date}</p>
                    <div className='Trackrecord-record'>
                      <p>Wins {eventRecord.wins} - {eventRecord.losses} Losses</p>
                    </div>
                    <p className={eventRecord.cumulative_units < 0 ? "red" : "green"}>Cumulative Units: {eventRecord.cumulative_units}</p>
                </div>
                )}
        </div>
    </div>
   </>
  );
}

export default Trackrecord;