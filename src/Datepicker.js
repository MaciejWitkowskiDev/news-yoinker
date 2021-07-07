import Form from 'react-bootstrap/Form'

const handleDatechange = (setter, event) => {
    setter(event.target.value);
}

const Datepicker = (props) => {
    return (
        <Form.Group className="mb-3">
            <Form.Label>{props.label}</Form.Label>
            <Form.Control type="date" onChange={(event) => handleDatechange(props.setter,event)}  max={new Date().toISOString().slice(0, 10)}/>
        </Form.Group>
    )
}

export default Datepicker;