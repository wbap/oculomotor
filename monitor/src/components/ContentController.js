import React from 'react'
import { connect } from 'react-redux'
import injectSheet from 'react-jss'
import _ from 'lodash'

import { sendContent } from '../actions'
import { controller } from '../styles'


const mapState = state => ({
  ...state.content,
})

const mapActions = dispatch => ({
  onClick: value => dispatch(sendContent(value)),
})

const ContentController = ({ classes, value, range, onClick }) => (
  <div className={classes.container}>
    {_.range(range).map(i => (
    <div
      className={i === value ? classes.focusedButton : classes.blurredButton}
      key={i}
      value={i}
      onClick={event => onClick(i)}
    >{i}</div>
    ))}
  </div>
)

export default connect(mapState, mapActions)(injectSheet(controller)(ContentController))
