import React, { Component } from 'react'
import { connect } from 'react-redux'

import ContentController from './ContentController'
import DifficultyController from './DifficultyController'

import { init, info, stepAgent } from '../actions'

const mapState = state => ({
  frame: state.frame,
})

const mapActions = dispatch => ({
  initialize: () => dispatch(init()),
  getInfo: () => dispatch(info()),
  callAgent: () => dispatch(stepAgent()),
})

class App extends Component {
  handler = undefined

  componentWillMount = () => {
    this.props.initialize()
    this.handler = setInterval(() => {
      this.props.getInfo().then(this.props.callAgent)
    }, 100)
  }

  componentWillUnmount =() => {
    clearInterval(this.handler)
  }

  render = () => (
    <div>
      <img alt="Agent Monitor" src={`data:image/png;base64,${this.props.frame}`} />
      <ContentController />
      <DifficultyController />
    </div>
  )
}

export default connect(mapState, mapActions)(App)
