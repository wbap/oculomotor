import React from 'react'
import { connect } from 'react-redux'
import injectSheet from 'react-jss'
import _ from 'lodash'

import { sendDifficulty } from '../actions'
import { controller } from '../styles'


const mapState = state => ({
  ...state.difficulty,
})

const mapActions = dispatch => ({
  onClick: value => dispatch(sendDifficulty(value)),
})

const DifficultyController = ({classes, value, range, onClick}) => (
  <div className={classes.container}>
    {_.range(-1, range).map(i => (
    <div
      className={i === value ? classes.focusedButton : classes.blurredButton}
      key={i}
      value={i}
      onClick={event => onClick(i)}
    >{i < 0 ? 'A' : i}</div>
    ))}
  </div>
)

export default connect(mapState, mapActions)(injectSheet(controller)(DifficultyController))
