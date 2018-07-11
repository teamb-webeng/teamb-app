import React, { Component } from 'react';
import {
  Button,
  Card,
  CardBody,
  CardTitle,
  Col,
  FormGroup,
  Input,
  Label,
  Row,
} from 'reactstrap';
import ClassNames from 'classnames';
import $ from 'jquery';


class Mypage extends Component {
  constructor(props) {
    super(props);

    this.onRadioBtnClick = this.onRadioBtnClick.bind(this);
    this.onSelectChange = this.onSelectChange.bind(this);
    this.onFileChange = this.onFileChange.bind(this);
    this.onSubmitClick = this.onSubmitClick.bind(this);

    this.state = {
      maxQuestionNumber: 10,
      radioSelected: 0,
      questionNumber: 1,
      setFile: false,
      canSubmit: false,
    };
  }

  onRadioBtnClick(radioSelected) {
    this.setState({
      radioSelected: radioSelected,
    });
    if (this.state.setFile) {
      this.setState({ canSubmit: true });
    }
  }

  onSelectChange(e) {
    this.setState({ questionNumber: parseInt(e.target.value, 10) });
  }

  onFileChange(e) {
    this.setState({ setFile: e.target.files[0] });
    if (this.state.radioSelected) {
      this.setState({ canSubmit: true });
    }
  }

  onSubmitClick() {
    const file = this.state.setFile
    const reader = new FileReader();
    reader.readAsText( file );

    let promise = new Promise((resolve, reject) => {
      const waiter = setInterval(function() {
        if (reader.readyState === 2) {
          clearInterval(waiter);
          $.ajax({
            url: '/api/savefile',
            type: 'GET',
            data: {
              data: reader.result,
              name: file.name,
            },
          }).done(() => {
            console.log('submit successful');
            resolve()
          });
        }
      }, 100);
    })

    promise.then(() =>{
      this.routeToResult()
    })
  }

  routeToResult() {
    this.props.history.push({
      pathname: "/result",
      state: {
        qNum: this.state.questionNumber,
        kind: this.state.radioSelected,
        filename: this.state.setFile.name,
      },
    })
  }

  render() {
    const list = [];
    [...Array(this.state.maxQuestionNumber)].map((_, i) =>
      list.push(<option key={`num${i}`} value={i+1}>{i+1}</option>)
    )

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
                        <Input type="radio" name="radio" onClick={() => this.onRadioBtnClick(1)} />{' '}
                          穴埋め自由回答形式
                      </Label>
                    </FormGroup>
                    <FormGroup check>
                      <Label check>
                        <Input type="radio" name="radio" onClick={() => this.onRadioBtnClick(2)} />{' '}
                          穴埋め選択回答形式
                      </Label>
                    </FormGroup>
                  </FormGroup>
                <FormGroup>
                  <Label for="Select">問題数:</Label>
                  <Input type="select" name="select" id="Select" onChange={(e) => this.onSelectChange(e)}>
                    {list}
                  </Input>
                </FormGroup>
                <FormGroup id="fileForm">
                  <Label for="exampleFile">問題を作成したいテキストファイル:</Label>
                  <Input type="file" name="file" id="exampleFile" onChange={(e) => this.onFileChange(e)}　/>
                </FormGroup>
                <Button className={ClassNames(
                    "btn-outline-dark",
                    {
                      "disabled": !this.state.canSubmit,
                    })}
                    onClick={() => this.onSubmitClick()}>送信</Button>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Mypage;
