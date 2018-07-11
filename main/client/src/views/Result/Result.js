import React, { Component } from 'react';
import {
  Card,
  CardBody,
  CardText,
  CardTitle,
  Col,
  Row,
} from 'reactstrap';
import $ from 'jquery';


class Result extends Component {
  constructor(props) {
    super(props);

    this.state = {
      ...this.props.location.state,
      questions: {}
    }
  }

  componentWillMount() {
    $.ajax({
      url: '/api/result',
      type: 'GET',
      dataType: 'json',
      data: { ...this.state },
    }).done((json) => {
      this.setState({ questions: json })
    });
  }

  render() {
    const list = [];
    [...Array(Object.keys(this.state.questions).length)].map((_, i) => {
      const question = this.state.questions[i]
      if (this.state.kind === 1) {
        list.push(<ResultCard data={{
          order: i + 1,
          question: question.question,
          answer: question.answer,
          }} />)
      }else if (this.state.kind === 2) {
        list.push(<ResultChoiceCard data={{
          order: i + 1,
          question: question.question,
          answer: question.answer,
          choices: question.choices,
          }} />)
      }
    })

    return (
      <div>
        {list}
      </div>
    );
  }
}

class ResultCard extends Component {
  constructor(props) {
    super(props);

    this.state = {
      order: this.props.data.order,
      question: this.props.data.question,
      answer: this.props.data.answer,
    }
  }

  render() {
    return (
      <div className="animated fadeIn">
        <Row>
          <Col xs="12" lg="8">
            <Card>
              <CardBody>
                <CardTitle>第{this.state.order}問</CardTitle>
                <CardText>問題:　{this.state.question}</CardText>
                <CardText>答え:　{this.state.answer}</CardText>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

class ResultChoiceCard extends Component {
  constructor(props) {
    super(props);

    this.state = {
      order: this.props.data.order,
      question: this.props.data.question,
      answer: this.props.data.answer,
      choices: this.props.data.choices,
    }
  }

  render() {
    const list = [];
    [...Array(Object.keys(this.state.choices).length)].map((_, i) => {
      list.push(<CardText className="mb-0">　{i+1}.　{this.state.choices[i]}</CardText>)
    })

    return (
      <div className="animated fadeIn">
        <Row>
          <Col xs="12" lg="8">
            <Card>
              <CardBody>
                <CardTitle>第{this.state.order}問</CardTitle>
                <CardText>問題:　{this.state.question}</CardText>
                <CardText>選択肢:</CardText>
                <CardText>{list}</CardText>
                <CardText>答え:　{this.state.answer + 1}.　{this.state.choices[this.state.answer]}</CardText>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Result;
