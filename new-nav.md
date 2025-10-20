The feature set (see `./instructions.md`) of this app is quite solid, but the UI is a bit incoherent and confusion.

Get rid of the current header and standardize to a breadcrumbs view on top.
On the very right of the header should be a settings icon to go a settings page, currently providing only a logout button.
Apart from that, the header should be breadcrumbs.

The left-most breadcrumbs item should always be "Curricula".
This should show the curricula (like `flashcards/curricula/` but much simplified, literally just the names and descriptions in a table, as well as links to edit and delete.

You can click on one's name (link), which moves the breadcrumbs display to "Curricula > $Curriculum_name" (all items in the breadcrumbs should ofc be link).

This page should list Subjects of this Curriculum, with a similar, non-nested tabular view.

And again, you can click on a name, goign to "Curricula > $curriculumn_name >  $subject_name", where again we have the same with topics.

topics is again quite the same, listing collections.

finally, a collection should list its flashcards and allow the implemented functinos such as csv upload. This is quite well implemented already (url `flashcards/collections/$id/`) and will need little change.

When editing a flashcard, we should keep using the breadcrumbs, in this case we're deep at
"Curricula > $curriculum_name > $suject_name > $topic_name > $collection_name > $flashcard_front (ellipisis)".