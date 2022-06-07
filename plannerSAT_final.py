from PDDL import PDDL_Parser
import numpy as np
import subprocess
import time




domain,problem='examples/grapple/grapple.pddl', 'examples/grapple/grapple_pb1.pddl'

class plannerSAT:

    def apply(self, state, positive, negative):
        return state.difference(negative).union(positive)

    def applicable( self, state, positive, negative):
        return positive.issubset(state) and negative.isdisjoint(state)


    def action2string(self,action):
        res=action.name+"."
        for x in action.parameters:
            res+=x+"."
        return(res)

    def predicate2string(self,predicate):
        res=""
        for x in predicate:
            res+=x+"."

        return(res)

    def solve(self,domain,problem):
        t0=time.time()
        parser = PDDL_Parser()
        parser.parse_domain(domain)
        parser.parse_problem(problem)

        variable_predicate=[]
        fixed_predicate=[]
        for pre in parser.predicates:
            used=False
            for act in parser.actions:
                for x in act.add_effects :
                    if x[0]==pre:
                        used=True
                        break
            if used:
                variable_predicate.append(pre)
            else:
                fixed_predicate.append(pre)
        verite=[]
        state=parser.state
        for x in state:
            if x[0] in fixed_predicate:

                verite.append(x)

        actions=[]


        for action in parser.actions:
            for act in action.groundify(parser.objects, parser.types):
                valide=True
                for x in act.positive_preconditions:
                    if x[0] in fixed_predicate:
                        if x not in verite:
                            valide=False
                            break
                for x in act.negative_preconditions:
                    if x[0] in fixed_predicate:
                        if x in verite:
                            valide=False
                            break

                if valide:
                    parameters=[]
                    for param in act.parameters:
                        if param not in parameters:
                            parameters.append(param)
                        else:
                            valide=False
                            break
                    if valide:
                        actions.append(act)


        index={}
        variable=[None]
        oldclause=[]
        oldpredicates=[]
        for predicate in parser.state:
            if predicate[0] in variable_predicate:
                oldpredicates.append(self.predicate2string(predicate))

        compteur=1
        for predicate in oldpredicates:
            index[predicate+"0"]=compteur
            variable.append(predicate+"0")
            oldclause.append([compteur])
            compteur+=1
        T=0
        while True:

            newclause=[]
            T+=1
            print("")
            print("etapes : "+str(T))
            newvariable=[]
            newpredicates=[]
            newactions=[]
            dict_pos_antecedant={}
            dict_neg_antecedant={}
            for action in actions:
                antecedant_pos=[]
                antecedant_neg=[]
                valide1=True
                for positive_precondition in action.positive_preconditions:
                    if positive_precondition[0] in variable_predicate:
                        valide2=False
                        for var_predicate in oldpredicates:
                            if var_predicate==self.predicate2string(positive_precondition):
                                antecedant_pos.append(var_predicate)
                                valide2=True
                                break
                        if not valide2:
                            valide1=False
                            break

                if valide1:
                    for negative_precondition in action.negative_preconditions:
                        if negative_precondition[0] in variable_predicate:
                            for var_predicate in oldpredicates:
                                if var_predicate==self.predicate2string(negative_precondition):
                                    antecedant_neg.append(var_predicate)

                    newactions.append(action)
                    variable_name=self.action2string(action)+str(T)
                    newvariable.append(variable_name)
                    index[variable_name]=compteur
                    k1=compteur
                    compteur+=1
                    for predicate in antecedant_pos:
                        newclause.append([-k1,index[predicate+str(T-1)]])
                    for predicate in antecedant_neg:
                        newclause.append([-k1,-index[predicate+str(T-1)]])
                    for positive_effect in action.add_effects:
                        predicate=self.predicate2string(positive_effect)
                        if predicate not in newpredicates:
                            newpredicates.append(predicate)
                            newvariable.append(predicate+str(T))
                            index[predicate+str(T)]=compteur
                            dict_pos_antecedant[compteur]=[]
                            dict_neg_antecedant[compteur]=[]
                            compteur+=1
                        k2=index[predicate+str(T)]
                        dict_pos_antecedant[index[predicate+str(T)]].append(k1)
                        newclause.append([-k1,k2])

            for predicate in oldpredicates:
                if predicate not in newpredicates:
                    newpredicates.append(predicate)
                    newvariable.append(predicate+str(T))
                    index[predicate+str(T)]=compteur
                    dict_pos_antecedant[compteur]=[]
                    dict_neg_antecedant[compteur]=[]
                    compteur+=1
            for action in newactions:
                k1=index[self.action2string(action)+str(T)]
                for negative_effect in action.del_effects:
                    predicate=self.predicate2string(negative_effect)
                    if predicate in newpredicates:
                        k2=index[predicate+str(T)]
                        dict_neg_antecedant[index[predicate+str(T)]].append(k1)
                        newclause.append([-k1,-k2])

            for i in range(len(newactions)):
                for j in range(i+1,len(newactions)):
                    ii=index[self.action2string(newactions[i])+str(T)]
                    jj=index[self.action2string(newactions[j])+str(T)]
                    newclause.append([-ii,-jj])

            for predicate in newpredicates:
                new=False
                i=index[predicate+str(T)]
                clause_pos=[-i]
                clause_neg=[i]
                if predicate in oldpredicates:
                    j=index[predicate+str(T-1)]
                    clause_pos.append(j)
                    clause_neg.append(-j)
                else:
                    new=True
                for k in dict_pos_antecedant[i]:
                    clause_pos.append(k)
                for k in dict_neg_antecedant[i]:
                    clause_neg.append(k)
                newclause.append(clause_pos)
                if not new:

                    newclause.append(clause_neg)







            oldpredicates=newpredicates
            variable+=newvariable

            oldclause+=newclause
            faisable=True
            g_pos=[]
            g_neg=[]
            for goal_pos in parser.positive_goals:
                if self.predicate2string(goal_pos) not in newpredicates:
                    faisable=False
                    break
                else:
                    g_pos.append(index[self.predicate2string(goal_pos)+str(T)])
            for goal_neg in parser.negative_goals:
                if self.predicate2string(goal_neg) in newpredicates:
                    g_neg.append(index[self.predicate2string(goal_neg)+str(T)])

            if not faisable:
                print("Pas encore de solution envisageable")
            else:
                goalclause=[]
                for k in g_pos:
                    goalclause.append([k])
                for k in g_neg:
                    goalclause.append([-k])
                myClauses= oldclause + goalclause
                print("nombre variables : "+str(len(variable)))
                print("nombre clauses : "+str(len(myClauses)))
                myDimacs = 'c This is it\np cnf '+str(len(variable)-1)+' '+str(len(myClauses))+'\n'
                for clause in myClauses :
                    for atom in clause :
                        myDimacs += str(atom) +' '
                    myDimacs += '0\n'
                with open("workingfile.cnf", "w", newline="") as cnf:
                    cnf.write(myDimacs)
                result = subprocess.run(["./gophersat.exe", "workingfile.cnf"], stdout=subprocess.PIPE, check=True, encoding="utf8")
                string = str(result.stdout)
                lines = string.splitlines()

                if lines[1] != "s SATISFIABLE":
                    print("Pas de solution")
                else:
                    print("Solution trouvée")
                    plan=[]
                    model = lines[2][2:].split(" ")
                    for t in range(T+1):
                        for action in actions:
                            if self.action2string(action)+str(t) in variable:
                                i=index[self.action2string(action)+str(t)]
                                if int(model[i-1])>0:
                                    plan.append(action)
                    t1=time.time()
                    print("plan trouvé : ")
                    for action in plan:
                        print(action)
                    print("temps : "+str(t1-t0))
                    print("nombre d'etapes : "+str(T))
                    return(plan)

    def check(self,domain,problem,plan):
        parser = PDDL_Parser()
        parser.parse_domain(domain)
        parser.parse_problem(problem)
        state=parser.state
        goal_pos = parser.positive_goals
        goal_not = parser.negative_goals
        for act in plan:
                if self.applicable(state, act.positive_preconditions, act.negative_preconditions):
                        state = self.apply(state, act.add_effects, act.del_effects)
                else:
                        return(False)
        if self.applicable(state, goal_pos, goal_not):
                return(True)
        else:
                return(False)
