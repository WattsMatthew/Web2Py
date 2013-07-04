def index():
    #defining Aliases
    Parent_alias=db_connect.Parent.with_alias('Parent_aliases')
    #defining query using left join
    query=(db_connect.Child.id>0)
    fields=[db_connect.Child.id,db_connect.Child.cname,db_connect.Parent.name,Parent_alias.name]
    #qery=db_connect().select(db_connect.Child.id,db_connect.Child.cname,db_connect.Parent.name,Parent_alias.name)
    left=[db_connect.Parent.on(db_connect.Child.mother==db_connect.Parent.id),
        Parent_alias.on(db_connect.Child.father==Parent_alias.id)]
    forms=SQLFORM.grid(query=query,fields=fields,left=left)
    return dict(forms=forms)
