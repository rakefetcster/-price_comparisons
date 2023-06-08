import { useState } from 'react';
import  '../App.css';
import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import axios from 'axios'
import { SpinnerCircular } from 'spinners-react';
import Alert from '@mui/material/Alert';

const serverUrl = 'http://localhost:5000/compares';
function CompareComp() {
  const [url,setUrl]=useState('');
  const [rowFile,setRowFile]=useState([]);
  const [header,setHeader]=useState([]);
  const [errorMassage,setErrorMassage]=useState([]);
  const [wait,setWait]=useState();
  const [error,setError]=useState(false);

  const linkEnter=async()=>{
    setWait(true);
    setError(false);
    const {data} = await axios.post(serverUrl,{"link":url});
    if (data.hasOwnProperty("Error")){
      setError(true);
      setErrorMassage(data['Error'])
      setWait('');
    }
    else{
    setHeader(data['header']);
    setRowFile(data['body']);
    setWait(false);
    }
  }
  

  return (
    <div>
    <div className='frameAll'>
    <div className='box'>
    <Box
    component="form"
    sx={{
      '& > :not(style)': { m: 1, width: '110ch' },
    }}
    noValidate
    autoComplete="off"
  >
  <TextField id="outlined-basic" label="Please Enter Full Link" variant="outlined" onChange={e=>setUrl(e.target.value)}/>
    
  </Box>
  </div>
  <div className='button'>
  <Stack spacing={1} direction="row" >
    
      <Button  variant="contained" size="large"   sx={{ width: 162, padding: 1 ,backgroundColor: '#ffcc66',height: 53 }} onClick={linkEnter}>Enter Link</Button>
    </Stack>
    </div>
  </div>
  <div>
  {error? <Stack sx={{ width: '100%' }} spacing={2}>
  <Alert severity="error">This is an error alert — check it out!
  {errorMassage}</Alert>
  
</Stack>:''} 
  {wait?<SpinnerCircular className='spinner' size={100} thickness={100} speed={100} color="#ffcc66" secondaryColor="rgba(0, 0, 0, 0.44)" />
  : 
  <table style={{border: "1px sold black"}}>
  <thead>
   <tr>
      {header.map((hed,key)=>{
        return(<th key={key}>{hed}</th>)
      })}
      </tr>
      </thead>
      <tbody>
      {rowFile.map((rowList,key)=>{
        return(
          <tr key={key}>
          {
            rowList.map((rowList,key1)=>{
              return(
              <td key={key1}>{rowList}</td>
              )
            })
          }
          </tr>
        )
          })}
       
     
      </tbody>
  </table> 
        }
 
  </div>
  

  </div>
  );
 
}

export default CompareComp;
