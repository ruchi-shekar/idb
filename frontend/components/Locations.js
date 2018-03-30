import React, { Component } from 'react';
//import chunk from 'lodash.chunk';
import {Router, Route, Link, RouteHandler, Redirect} from 'react-router';

class Locations extends Component {

constructor (props) {
    super(props);
    this.state = {
      locations: [],
      navigate: false,
      navigateTo: '',
      selectedLocation: [],
      navigateTo: "",
      item: "",
      currentPage: 1,
      locationsPerPage: 9,
      cities_list: []
    };
};

componentDidMount(props) {
    fetch('/getsceniclocations').then(results =>{
      console.log(results)
      return results.json();
    }).then(data =>{
      console.log(data)
      let views = data.map((scenicloc) =>{
        return(
        <div id="location_instance" key={scenicloc.scenic_name} onClick={() =>{this.setState({navigate: true, navigateTo: "/location", selectedLocation: scenicloc})}}>
          <li className="col">
              <img src={scenicloc.scenic_picture} style={{width: 300, height: 300}} alt="Photo1"
              />
              <span className="picText">
                <span><b>{scenicloc.scenic_name}</b>
                <br /><br />{scenicloc.scenic_address}
                <br />{scenicloc.scenic_rating + "/5"}
                </span>
              </span>
          </li>
        </div>
      )
    })
    this.setState({locations: views});
  })
  this.getCities();
}

getCities() {
  fetch('/getcities').then(results =>{
    console.log(results)
    return results.json();
  }).then(data=>{
    console.log(data)
    let cities = data.map((city) =>{
      return(
        <li><a href="#">{city.city_name}</a></li>
      )
    })
    this.setState({cities_list: cities});
  })
}

handleClick(event) {
    this.setState({
      currentPage: Number(event.target.id)
    });
  }

render() {

  const{locations, currentPage, locationsPerPage} = this.state;

  const indexOfLastLocation = currentPage * locationsPerPage;
  const indexOfFirstLocation = indexOfLastLocation - locationsPerPage;
  const currentLocations = locations.slice(indexOfFirstLocation, indexOfLastLocation);

  const pageNumbers = [];
  for (let i = 1; i <= Math.ceil(locations.length / locationsPerPage); i++) {
    pageNumbers.push(i);
  }

  if (this.state.navigate) {
    console.log("REDIRCT" + this.state.selectedLocation);
    return <Redirect to={{pathname: this.state.navigateTo, state: {selectedLocation: this.state.selectedLocation}}} push={true} />;
  }

  const renderLocations = currentLocations.map((locations, index) => {
    return <li key={index}>{locations}</li>;
  });

  const renderPageNumbers = pageNumbers.map(number => {
    return (
      <li
        key={number}
        id={number}
        onClick={this.handleClick.bind(this)}
      >
        {number}
      </li>
    );
  });

  return (
      <div>
        {/*location dropdown*/}
        <div className="filters-and-grid">
        <div className="filter-container">
          <div className="dropdown">
            <button id="city-btn" className="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Choose a City to Explore
              <span className="caret" /></button>
            <ul className="dropdown-menu" x-placement="bottom-start">
              {this.state.cities_list}
            </ul>
          </div>
        </div>
        <section className="page-section">
          <div className="container">
            <div className="row">
              <ul className="img-list">
                <div className="row">
                  {renderLocations}
                </div>
              </ul>
            </div>
          </div>
        </section>
        </div>
        <div className="col-md-12 text-center">
        <ul className="page-list">
          {renderPageNumbers}
        </ul>
        </div>
      </div>
    );
  }
}


export default Locations;
