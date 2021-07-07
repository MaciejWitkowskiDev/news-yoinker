import Nav from './Nav';
import NewsForm from './NewsForm';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import React, { useState } from 'react';

const App = () => {
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [phrases, setPhrases] = useState([]);
  return (
    <>
      <Nav />
      <Container fluid>
        <Row style={{padding: '50px'}}>
          <Col>
            <h1>Yoink the news...</h1>
            <NewsForm setStart={setStart} setEnd={setEnd} setPhrases={setPhrases}/>
          </Col>
          <Col>{start} {end}</Col>
        </Row>
      </Container>
    </>
  );
}

export default App;
