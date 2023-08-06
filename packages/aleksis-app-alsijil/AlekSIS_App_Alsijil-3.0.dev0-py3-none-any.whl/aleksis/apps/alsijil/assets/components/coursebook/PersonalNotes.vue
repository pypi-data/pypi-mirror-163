<template>
    <v-dialog
      v-model="dialog"
      max-width="600px"
      @click:outside="cancelDialog"
    >
      <template v-slot:activator="{ on, attrs }">
        <div>
          <template v-for="personalNote in personalNotes">
            <v-chip class="ma-1" close @click="editPersonalNote(personalNote.person.id)"
              @click:close="removePersonalNote(personalNote.person.id)" v-if="personalNoteString(personalNote)">
              {{ personalNote.person.fullName }}: {{ personalNoteString(personalNote) }}
            </v-chip>
          </template>
        </div>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              class="ma-1"
              color="primary"
              icon
              outlined
              v-bind="attrs"
              v-on="on"
              @click="createPersonalNote"
            >
              <v-icon>
                mdi-plus
              </v-icon>
            </v-btn>
          </template>
          <span v-text="$root.django.gettext('Add personal note')"></span>
        </v-tooltip>
      </template>
      <v-card>
        <v-card-title>
          <span class="text-h5">Personal Note</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-select
              item-text="fullName"
              item-value="id"
              :items="persons"
              label="Student"
              v-model="editedPersonID"
              @input="updatePersonalNote"
            ></v-select>
            <v-text-field
              label="Tardiness"
              suffix="min" type="number"
              min="0"
              :disabled="editedPersonID === ID_NO_PERSON"
              v-model="editedTardiness"
            ></v-text-field>
            <v-checkbox
              label="Absent"
              v-model="editedAbsent"
              :disabled="editedPersonID === ID_NO_PERSON"
              @change="editedExcused = false; editedExcuseType = null"
            ></v-checkbox>
            <v-checkbox
              label="Excused"
              v-model="editedExcused"
              :disabled="editedPersonID === ID_NO_PERSON || !editedAbsent"
              @change="editedExcuseType = null"
            ></v-checkbox>
            <v-select
              label="Excuse Type"
              v-model="editedExcuseType"
              :items="excuseTypes"
              item-text="name"
              return-object
              :disabled="editedPersonID === ID_NO_PERSON || !editedAbsent || !editedExcused"
            ></v-select>
            <v-select
              label="Extra Marks"
              v-model="editedExtraMarks"
              :items="extraMarks"
              item-text="name"
              return-object
              :disabled="editedPersonID === ID_NO_PERSON"
              multiple
              chips
            ></v-select>
            <v-text-field
              label="Remarks"
              v-model="editedRemarks"
              :disabled="editedPersonID === ID_NO_PERSON"
            ></v-text-field>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="error"
            outlined
            @click="cancelDialog"
          >
            Cancel
          </v-btn>
          <v-btn
            color="success"
            @click="saveDialog"
            :disabled="editedPersonID === ID_NO_PERSON"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
import gql from 'graphql-tag';

const ID_NO_PERSON = null;

export default {
    model: {
        prop: "personalNotes",
        event: "change",
    },
    created() {
        this.ID_NO_PERSON = ID_NO_PERSON;
    },
    methods: {
        removePersonalNote(personID) {
            if (personID === ID_NO_PERSON) {
                return
            }
            console.log("removing personal note of person", personID);
            this.editedPersonID = personID;
            this.editedTardiness = 0;
            this.editedAbsent = false;
            this.editedExcused = false;
            this.editedExcuseType = null;
            this.editedExtraMarks = [];
            this.editedRemarks = "";

            this.savePersonalNote();
        },
        editPersonalNote(personID) {
            console.log("editing personal note of person", personID);
            this.editedPersonID = personID;
            this.updatePersonalNote();
            this.dialog = true;
        },
        updatePersonalNote() {
            let personalNote = this.personalNoteByStudentID(this.editedPersonID);
            this.editedTardiness = personalNote.late || 0;
            this.editedAbsent = personalNote.absent || false;
            this.editedExcused = personalNote.excused || false;
            this.editedExcuseType = personalNote.excuseType || null;
            this.editedExtraMarks = personalNote.extraMarks || [];
            this.editedRemarks = personalNote.remarks || "";

            this.newPersonalNote = !!(personalNote && Object.keys(personalNote).length === 0 && Object.getPrototypeOf(personalNote) === Object.prototype);
        },
        createPersonalNote() {
            this.editedPersonID = ID_NO_PERSON;
            this.editedTardiness = 0;
            this.editedAbsent = false;
            this.editedExcused = false;
            this.editedExcuseType = null;
            this.editedExtraMarks = [];
            this.editedRemarks = "";
            this.newPersonalNote = true;
            this.dialog = true;
        },
        personalNoteByStudentID(studentID) {
            if (this.editedPersonID === ID_NO_PERSON) {
                return {};
            }
            return this.personalNotes.filter(item => item.person.id === studentID)[0] || {};
        },
        savePersonalNote() {
            if (this.editedPersonID === ID_NO_PERSON) {
                return
            }

            let editedExcuseTypeID = (this.editedExcuseType) ? this.editedExcuseType.id : null;
            let editedExtraMarksIDs = [];
            this.editedExtraMarks.forEach(item => {editedExtraMarksIDs.push(item.id);});

            // We save the user input in case of an error
            const variables = {
                "personId": this.editedPersonID,
                "late": this.editedTardiness,
                "absent": this.editedAbsent,
                "excused": this.editedExcused,
                "excuseType": editedExcuseTypeID,
                "extraMarks": editedExtraMarksIDs,
                "remarks": this.editedRemarks,
                "lessonDocumentation": this.lessonDocumentationId,
            }

            console.log(variables)

            // Call to the graphql mutation
            this.$apollo.mutate({
                // Query
                mutation: gql`mutation updateOrCreatePersonalNote(
                    $personId: ID!,
                    $lessonDocumentation: ID!,
                    $late: Int,
                    $absent: Boolean,
                    $excused: Boolean, 
                    $excuseType: ID, 
                    $extraMarks: [ID],
                    $remarks: String
                ) {
                    updateOrCreatePersonalNote(personId: $personId,
                        lessonDocumentation: $lessonDocumentation,
                        late: $late,
                        absent: $absent,
                        excused: $excused,
                        excuseType: $excuseType,
                        extraMarks: $extraMarks,
                        remarks: $remarks
                    ) {
                        personalNote {
                            id
                            person {
                                id
                                fullName
                            }
                            late
                            remarks
                            absent
                            excused
                            excuseType {
                                id
                            }
                            extraMarks {
                                id
                            }
                        }
                    }
                }
                `,
                // Parameters
                variables: variables,
            }).then((data) => {
                // Result
                console.log(data)
                // FIXME: check if data changed (?), display success message
            }).catch((error) => {
                // Error
                console.error(error)
                // FIXME: Notify the user about the error, maybe retry
            })

            if (this.newPersonalNote) {
                this.personalNotes.push({
                    person: {
                        id: this.editedPersonID,
                        fullName: this.studentNameByID(this.editedPersonID)
                    },
                    tardiness: this.editedTardiness,
                    absent: this.editedAbsent,
                    excused: this.editedExcused,
                    excuseType: this.editedExcuseType,
                    extraMarks: this.editedExtraMarks,
                    remarks: this.editedRemarks,
                });
            } else {
                // Loop through all personal notes and update the ones that match the editedPersonID
                this.personalNotes.forEach(item => {
                    if (item.person.id === this.editedPersonID) {
                        item.tardiness = this.editedTardiness;
                        item.absent = this.editedAbsent;
                        item.excused = this.editedExcused;
                        item.excuseType = this.editedExcuseType;
                        item.extraMarks = this.editedExtraMarks;
                        item.remarks = this.editedRemarks;
                    }
                });
            }
            this.$emit('change', this.personalNotes)
        },
        cancelDialog() {
            this.dialog = false;
            this.editedPersonID = ID_NO_PERSON;
        },
        saveDialog() {
            this.savePersonalNote();
            this.dialog = false;
            this.editedPersonID = ID_NO_PERSON;
        },
        personalNoteString(personalNote) {
            let personalNoteString = "";
            if (personalNote.late > 0) {
                personalNoteString += personalNote.late + " min. ";
            }
            if (personalNote.absent) {
                personalNoteString += "abwesend ";
            }
            if (personalNote.excused) {
                personalNoteString += "entschuldigt ";
            }
            if (personalNote.excuseType) {
                personalNoteString += personalNote.excuseType.name;
            }
            if (personalNote.extraMarks.length > 0) {
                personalNoteString += " (";
                personalNote.extraMarks.forEach(item => {
                    personalNoteString += item.name + ", ";
                });
                personalNoteString = personalNoteString.substring(0, personalNoteString.length - 2);
                personalNoteString += ") ";
            }
            if (personalNote.remarks) {
                personalNoteString += "\"" + personalNote.remarks + "\" ";
            }
            return personalNoteString;
        },
        studentNameByID(studentID) {
            try {
                return this.persons.filter(item => item.id === studentID)[0].fullName;
            } catch (TypeError) {
                return "";
            }
        }
    },
    props: ["lessonDocumentationId", "personalNotes", "groups", "excuseTypes", "extraMarks"],
    name: "personal-notes",
    data: () => {
        return {
            dialog: false,
            // Absent versp. exc. type hw note
            editPersonalNoteId: null,
            editedPersonID: ID_NO_PERSON,
            editedTardiness: 0,
            editedAbsent: false,
            editedExcused: false,
            editedExcuseType: null,
            editedExtraMarks: [],
            editedRemarks: "",
            newPersonalNote: false,
        }
    },
    computed: {
        persons() {
            // go through each group and get the students
            // use the group names as headers for the v-select

            return this.groups.map(
                group => {
                    return [
                        {header: group.name, id: group.shortName},
                        group.members
                    ]
                }
            ).flat(2);
        }
    }
}
</script>
