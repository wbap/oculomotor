export const BUTTON_SIZE = 20

export const controller = {
  container: {
    clear: 'left',
  },
  focusedButton: {
    float: 'left',
    width: BUTTON_SIZE-2,
    height: BUTTON_SIZE-2,
    backgroundColor: 'blue',
    color: 'white',
    border: 'solid 1px black',
  },
  blurredButton: {
    float: 'left',
    width: BUTTON_SIZE-2,
    height: BUTTON_SIZE-2,
    backgroundColor: 'white',
    color: 'black',
    border: 'solid 1px black',
  },
}
