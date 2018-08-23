import { connect } from 'react-redux'
import Monitor from './Monitor'

const mapStateToProps = state => ({ content: state.content })
const mapDispatchToProps = dispatch => ({})

export default connect(mapStateToProps, mapDispatchToProps)(Monitor)
