import React from 'react'
import "../pages/CSS/About.css"; 

export default function About() {
    return (
        <div className='About'>
        <div className="About-container">
            <h1>About This Project</h1>
            <div className="About-text">
                <p>
                    I am an avid fan of the UFC and have watched all cards dating back to 2021. I utilized fastai's deep learning library to create a model to predict fight durations given a variety of inputs. I scraped all the model's training data and information to display in the UI using Scrapy.
                </p>
                <p>
                    The tech stack used in this project includes React for the front end and Flask for backend calls. This combination allows for a responsive and dynamic user experience while leveraging powerful machine learning capabilities on the server side.
                </p>
                <p>
                    You can find the source code and contribute to this project on GitHub: <a href="https://github.com/ay3xqa/myUFCAndPortfolio" target="_blank" rel="noopener noreferrer">myUFCAndPortfolio</a>.
                </p>
                <span className="About-update">Last updated on: 8/11/24</span>
            </div>
        </div>
        </div>
    );
}

