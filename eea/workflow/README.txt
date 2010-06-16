Workflow guards and readiness checking
--------------------------------------

We have the following use case:

 * objects of type "Specification" have several requirements that need to be
 * met before they can be published. 
	For example, some of their fields are not required in Archetypes sense, but
	they should be filled in before the object can be published. Also, several
	relations need to be created between a Specification and several other
	content types, in order to allow the transition to published.

We have implemented the following facilities that allow the above requirements
to be filled in:

 * now you can (should) add a boolean attribute called "required_for_zzz" field
   schema definitions, where zzz is the name of a workflow state. There is no 
	 code to enable this, because you can already
	 pass arbitrary parameters to AT Field definitions and they'll be stored in
	 the field.
 * we have a view called ``get_readiness``, registered for objects implementing 
	 ``eea.workflow.interfaces.IHasMandatoryWorkflowFields``. You can call this
	 view in a TALES expression like this: 
	 ``python:not path('here/@@get_readiness').is_ready_for('published')``
	 This view offers two methods: ``is_ready_for`` and ``get_info_for``. They
	 both accept a single parameter, the state name, and return a boolean or a
	 mapping with information. See code for this.
 * we have a portlet called portlet_readiness. Attach it to your objects and it
   will present the info that results from calling
	 ObjectReadiness.get_info_for()

The ObjectReadiness.is_ready_for() method can be used in workflow transitions
in the following fashion: let's assume that we want to guard the "published"
state with checks based on the required_for_published parameters passed to some
of the fields. Now we can add this expression as guard for the publish 
transition:

	 ``python:path('here/@@get_readiness').is_ready_for('published')``

If not all the mandatory fields are filled in, the object is not ready to be
published and the publish transition will be hidden. In our case, we want to
show the publish transition regardless of this check. We will create a new
transition called fake_publish, similar to the publish transition (and available
in all states where the publish transition is available). This transition is guarded
by this expression:

	 ``python:not path('here/@@get_readiness').is_ready_for('published')``
	
The fake_transition needs to stay in the same state when triggered, and needs to have
the eea.workflow.workflow_scripts.fake_transition set as before script.

If so configured, the fake publish transition will appear whenever the real publish 
transition is not available, and instead of publishing the object, it will redirect
to the object's view action and will display a portal message saying that the object
is not ready to be published.

NOTE: at this moment there are two conflicting portal messages that will appear: one, 
as explained above, and another one saying that the "object status has been succesfully
modified". Maybe we can do something about this?
