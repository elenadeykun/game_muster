import React from 'react';
import { Link } from 'react-router';
import PropTypes from 'prop-types';

class MainLayout extends React.Component{

  render() {
    return (
        <div>
          {this.props.children}
        </div>
    );
  }
}

export default MainLayout;
