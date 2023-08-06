<template>
  <ApolloMutation
      :mutation="require('./LessonDocumentation.graphql')"
      :variables=lessonDocumentationEdit
      @done="onDone"
  >
    <template v-slot="{ mutate, loading, error }">
      <v-card elevation="2" :loading="loading">
        <v-form v-model="valid">
          <v-card-title v-if="saveLessonDocumentationsPerWeek === 'True'">
            <span
              v-text="getWeekText(lessonDocumentationEdit)"
              class="ma-1 text-h5">
            </span>
          </v-card-title>
          <v-card-title v-else>
            <v-hover v-slot="{ hover }">
              <div>
                <v-menu
                    v-model="showPicker"
                    :close-on-content-click="false"
                    transition="scale-transition"
                    offset-y
                    min-width="auto"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <span>
                      <span
                          v-text="new Date(lessonDocumentationEdit.date).toLocaleDateString($root.languageCode)"
                          class="ma-1 text-h5"></span>
                      <v-btn right v-bind="attrs" v-on="on" icon
                             v-if="hover && dateAndPeriodEditable">
                        <v-icon>mdi-pencil-outline</v-icon>
                      </v-btn>
                    </span>
                  </template>
                  <v-date-picker
                      scrollable
                      no-title
                      @input="showPicker = false; $emit('change-date', $event)"
                      v-model="lessonDocumentationEdit.date"
                  ></v-date-picker>
                </v-menu>
              </div>
            </v-hover>
            <v-hover v-slot="{ hover }" v-if="!(saveLessonDocumentationsPerWeek === 'True')">
              <div>
                <v-menu offset-y>
                  <template v-slot:activator="{ on, attrs }">
                    <span>
                      <span
                          v-text="$root.django.gettext('Period') + ' ' + lessonDocumentationEdit.period"
                          class="ma-1 text-h5"></span>
                      <v-btn
                          right
                          v-bind="attrs"
                          v-on="on"
                          icon
                          v-if="hover && dateAndPeriodEditable"
                      >
                        <v-icon>mdi-pencil-outline</v-icon>
                      </v-btn>
                    </span>
                  </template>
                  <v-list>
                    <!-- Fixme: load valid lessons -->
                    <v-list-item
                        v-for="(item, index) in [1, 2, 3, 4, 5, 6, 7, 8, 9]"
                        :key="index"
                    >
                      <v-list-item-title>{{ item }}</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </div>
            </v-hover>
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="12" lg="12">
                <message-box type="error" v-if="error">Error updating data</message-box>
                <v-textarea
                    name="input-7-1"
                    :label="$root.django.gettext('Topic')"
                    rows="1"
                    auto-grow
                    required

                    v-model="lessonDocumentationEdit.topic"
                ></v-textarea>
                <v-textarea
                    name="input-7-1"
                    :label="$root.django.gettext('Homework')"
                    rows="1"
                    auto-grow

                    v-model="lessonDocumentationEdit.homework"
                ></v-textarea>
                <v-textarea
                    name="input-7-1"
                    :label="$root.django.gettext('Group note')"
                    rows="1"
                    auto-grow

                    v-model="lessonDocumentationEdit.groupNote"
                ></v-textarea>
              </v-col>
              <v-col v-if="!(saveLessonDocumentationsPerWeek === 'True')" cols="12" md="4" lg="4">
                Personal notes
                <personal-notes
                    :lesson-documentation-id="lessonDocumentationEdit.id"
                    :groups="groups"
                    :excuse-types="excuseTypes"
                    :extra-marks="extraMarks"

                    v-model="lessonDocumentationEdit.personalNotes"
                    @change="$emit('change-personal-notes', $event)"
                ></personal-notes>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                color="error"
                outlined
                @click="$emit('cancel-lesson-documentation-dialog', $event)"
            >
              {{ $root.django.gettext('Cancel') }}
            </v-btn>
            <v-btn
                color="success"
                @click="mutate()"
            >
              {{ $root.django.gettext('Save') }}
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </template>
  </ApolloMutation>
</template>

<script>
import PersonalNotes from "./PersonalNotes.vue";

export default {
  components: {PersonalNotes},
  props: ["lessonDocumentationEdit", "groups", "excuseTypes", "extraMarks", "saveLessonDocumentationsPerWeek", "getWeekText"],
  name: "lesson-documentation",
  data() {
    return {
      dateAndPeriodEditable: false,
      showPicker: false,
      //lessonDocumentationEdit: {},
    }
  },
  //created() {
  //this.lessonDocumentationEdit = this.lessonDocumentation
  //}
}
</script>
