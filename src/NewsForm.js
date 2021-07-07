import Form from 'react-bootstrap/Form';
import Datepicker from './Datepicker';


const NewsForm = (props) => {
    return(
        <>
        <Form>
            <Datepicker setter={props.setStart} label="From" />
            <Datepicker setter={props.setEnd} label="To" />
            <Form.Group className="mb-3">
                <Form.Label>Containing phrases: (enter comma separated)</Form.Label>
                <Form.Control as="textarea"  style={{height: '200px'}}/>
            </Form.Group>
        </Form>
        </>
    );
}

export default NewsForm