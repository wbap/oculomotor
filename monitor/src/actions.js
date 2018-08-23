import { step } from './api'

export const nextContent = () => ({ type: 'NEXT_CONTENT' })
export const prevContent = () => ({ type: 'PREV_CONTENT' })

const updateFrame = image => ({ type: 'UPDATE_FRAME', image })
export const stepAgent = () => dispatch => step().then(response => response.text()).then(image => dispatch(updateFrame(image)))
