import React, { Component } from 'react';
import {
  Button,
  Card,
  CardBody,
  CardHeader,
  CardTitle,
  Col,
  FormGroup,
  Input,
  Label,
  Row,
} from 'reactstrap';


class Mypage extends Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.onRadioBtnClick = this.onRadioBtnClick.bind(this);

    this.state = {
      dropdownOpen: false,
      radioSelected: 2,
    };
  }

  toggle() {
    this.setState({
      dropdownOpen: !this.state.dropdownOpen,
    });
  }

  onRadioBtnClick(radioSelected) {
    this.setState({
      radioSelected: radioSelected,
    });
  }

  render() {
    return (
      <div className="animated fadeIn">
        <Row>
          <Col xs="12" lg="8">
            <Card>
              <CardBody>
                <CardTitle>hello administrator!</CardTitle>
                <FormGroup>
                  <legend className="col-form-label">問題形式選択:</legend>
                    <FormGroup check>
                      <Label check>
                        <Input type="radio" name="radio" />{' '}
                          穴埋め自由回答形式
                      </Label>
                    </FormGroup>
                    <FormGroup check>
                      <Label check>
                        <Input type="radio" name="radio" />{' '}
                          穴埋め選択回答形式
                      </Label>
                    </FormGroup>
                  </FormGroup>
                <FormGroup>
                  <Label for="exampleSelect">問題数:</Label>
                  <Input type="select" name="select" id="exampleSelect">
                    <option>1</option>
                    <option>2</option>
                    <option>3</option>
                    <option>4</option>
                    <option>5</option>
                  </Input>
                </FormGroup>
                <FormGroup>
                  <Label for="exampleFile">問題を作成したいテキストファイル:</Label>
                  <Input type="file" name="file" id="exampleFile" />
                </FormGroup>
                <Button className="btn-outline-dark">送信</Button>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Mypage;
