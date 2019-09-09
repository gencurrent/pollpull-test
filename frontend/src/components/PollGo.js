import React from 'react';
import Cookies from 'js-cookie';


class PollGo extends React.Component{

    state = {
        questionIdCurrent: null,
        answerIdCurrent: null,
        question: {
            id: null, 
            text: null,
            answerList: [],
        }
    }

    constructor(props){
        super(props);
        this.pollId = this.props.match.params.id;
        this.udpateQuestion = this.udpateQuestion.bind(this);
        this.submitAnswer = this.submitAnswer.bind(this);
        this.buttonNextClicked = this.buttonNextClicked.bind(this);
        this.answerChanged = this.answerChanged.bind(this);
    }

    updatePollStatus(){
        const pollUrl = `/api/poll/${this.pollId}/`;
        fetch(pollUrl)
            .then(response => {
                if (response.status !== 200){
                    throw Error(`The status code in poll request is ${response.status}`)
                }
                return response.json();
            })
            .then(result => {
                const questionIdCurrent = result.questionAwaiting;
                this.setState({questionIdCurrent: questionIdCurrent}, this.udpateQuestion(questionIdCurrent));
            })
    }

    udpateQuestion(questionId){
        let url = `/api/question/${questionId}/`;
        fetch(url)
            .then(response => {
                if (response.status !== 200){
                    throw Error('200')
                }
                return response.json();
            })
                .then(result => {
                    const questionState = {question: result};
                    this.setState(questionState);
                })
                
    }

    answerChanged(event){
        const answerId = parseInt(event.target.value);
        this.setState({answerIdCurrent: answerId});
    }

    buttonNextClicked(event){
        event.preventDefault();
        const answerId = parseInt(this.state.answerIdCurrent);
        this.submitAnswer(answerId);
    }

    submitAnswer(answerId){
        let url = `/api/question/${this.state.question.id}/submit-answer/`;
        let pollId = this.state.pollId;
        let csrftoken = Cookies.get('csrftoken')
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken, 
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                answerId: answerId
            })
            
        })
            .then(response => {
                if (response.status !== 200){
                    throw Error("The error")
                }
                return response.json();
            })
            .then(result => {
                if (result.hasOwnProperty('finished') && result.finished == true){
                    let { history } = this.props;
                    history.push({
                     pathname: `/poll-result/${this.props.match.params.id}`,
                    });
                   
                }
                else{
                    const newState = {
                        answerIdCurrent: null,
                        questionIdCurrent: result.id,
                        question: result, 
                    }
                    this.setState(newState);
                }
            })
        ;
        
            
    }

    componentDidMount(){
        this.updatePollStatus();
    }

    render(){
        return (
            <div questionid={this.state.question.id} className='question-text'>
                <div className='question-text'>
                    {this.state.question.text}
                </div>
                <div className='question-option-list'>
                    <div className="form-check"> 
                    {
                        this.state.question.answerList.map(option => {
                            const randId = Math.random().toString(36).substring(2, 15);
                            
                            return (
                                <div>
                                    <input 
                                        className="form-check-input" 
                                        type="checkbox" answerId={option.id} 
                                        checked={this.state.answerIdCurrent === option.id}
                                        onChange={this.answerChanged}
                                        defaultValue={option.id} 
                                        id={randId} />
                                    <label className="form-check-label" htmlFor={randId}>
                                        {option.text}
                                    </label>
                                </div>
                            );
                        })
                    }
                    </div>
                </div>
                <button className="btn-submit" onClick={this.buttonNextClicked}>Далее</button>
            </div>
        )
    }
}


export default PollGo;