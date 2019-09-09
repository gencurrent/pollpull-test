"""
Файл функций для работы с БД 
"""

from django.db import connection

def get_poll_answers(poll_id):
    if type(poll_id) is not int:
        raise TypeError(f'The poll_id must be integer')
    raw_query = f"""
        WITH RECURSIVE answer_answergiven AS (
            SELECT 
                p_a_ag.*
            FROM
                    (SELECT 
                        p_ag.id                 answer_given_id,
                        p_a.id                  answer_id, 
                        p_a.question_id         question_id, 
                        p_a.question_lead_to_id question_lead_to_id,
                        p_ag.poll_id            poll_id,
                        p_a.grade
                    FROM 
                        poll_answergiven p_ag INNER JOIN poll_answer p_a ON (p_ag.answer_id = p_a.id)
                    ) p_a_ag
                LEFT JOIN 
                        poll_question p_q ON p_q.id = p_a_ag.question_id  
            WHERE p_a_ag.poll_id = {poll_id}

            UNION 

            SELECT 
                p_a_ag.*
            FROM
                    (SELECT 
                        p_ag.id                 answer_given_id,
                        p_a.id                  answer_id, 
                        p_a.question_id         question_id, 
                        p_a.question_lead_to_id question_lead_to_id,
                        p_ag.poll_id            poll_id,
                        p_a.grade
                        
                    FROM 
                        poll_answergiven p_ag INNER JOIN poll_answer p_a ON (p_ag.answer_id = p_a.id)
                    ) p_a_ag
                LEFT JOIN 
                        poll_question p_q ON p_q.id = p_a_ag.question_id  
            INNER JOIN answer_answergiven ON (p_a_ag.question_lead_to_id = answer_answergiven.question_id)
        )
        SELECT * FROM answer_answergiven """
        
    with connection.cursor() as c:
        c.execute(raw_query)
        result = c.fetchall()
    zipped = []
    columns = ('answer_given_id', 'answer_id', 'question_id', 'question_lead_to_id', 'poll_id', 'grade')
    for r in result:
        zipped.append(dict(zip(columns, r)))
    return zipped
            