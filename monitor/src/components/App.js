import React, { Component } from 'react'
import { connect } from 'react-redux'

import Monitor from './Monitor'

import { nextContent, prevContent } from '../actions'

const mapStateToProps = state => ({ content: state.content })

const mapDispatchToProps = dispatch => ({
  onClickNext: () => dispatch(nextContent()),
  onClickPrev: () => dispatch(prevContent()),
})

const App = ({ content, onClickNext, onClickPrev }) => (
  <div>
    <Monitor content={content} />
    <input type="button" value="前タスク" onClick={onClickPrev} />
    <input type="button" value="次タスク" onClick={onClickNext} />
  </div>
)

export default connect(mapStateToProps, mapDispatchToProps)(App)
