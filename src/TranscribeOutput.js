import React from "react";
import withStyles from "@material-ui/core/styles/withStyles";
import Typography from "@material-ui/core/Typography";


const useStyles = theme => ({
  root: {}
});

const TranscribeOutput = ({classes, currentData}) => {

  return (
    <div className={classes.root}>
      <Typography>Output: {currentData}</Typography>
    </div>
  )
}

export default withStyles(useStyles)(TranscribeOutput);
