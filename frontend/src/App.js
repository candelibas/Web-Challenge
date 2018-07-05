import React, { Component } from 'react';
import socketIOClient from 'socket.io-client';
import './App.css';

const courseId = 1178124;
const endpoint = 'http://localhost:9000';

class App extends Component {

  state = {
    reviews: [{}],
    course_title: '',
    date: ''
  }

  componentDidMount() {
    // Socket.io connection to get data and re-render component automatically
    const socket = socketIOClient(endpoint)
    socket.on('connect', () => console.log('Client connected!'))

    socket.on('message', (data) => {
      let result = data.split(","); // 0: avg_rating, 1: course_title, 2: date 3: time
      this.setState({
        reviews: [...this.state.reviews, { avg_rating: 'Avg Rating: ' + result[0], time: 'Hour: ' + result[3] + ' - ' }],
        course_title: result[1],
        date: result[2]
      });
      console.log(this.state.reviews);
    })

    socket.on('new_review', (data) => {
      // setting the color of our button
      console.log('hello:' + data);
    })
  }

  render() {
    const listReviews = this.state.reviews.map((rev) =>
        <p><span style={{fontWeight: 'bold'}}>{rev.time} </span> <span style={{color: "green"}}>{rev.avg_rating}</span></p>
    );
    return (
      <div className="App">
        <header className="App-header">
          <img src="https://discourse-cdn-sjc1.com/business5/uploads/gamedev/optimized/1X/2d1f1721ff9a04b33e75ce2e606e124626104249_1_690x149.png" className="App-logo" alt="logo" />
          <h1 className="App-title">Course Review Performance</h1>
        </header>
        <h2 className="App-intro">{this.state.course_title}</h2>
        <h3 className="App-intro">Daily Reviews(<span style={{color: "#9CDCFE"}}>{this.state.date}</span>)</h3>
        <p>
          { listReviews }
        </p>
      </div>
    );
  }
}

export default App;
