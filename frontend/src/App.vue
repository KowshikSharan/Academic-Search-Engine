<template>
  <v-app id="inspire">
    <v-app-bar app clipped-left>
      <!-- <v-app-bar-nav-icon @click.stop="drawer = !drawer" /> -->
      <v-icon>mdi-book-search</v-icon>
      <v-toolbar-title style="padding-left: 15px;"> Elastic Search on DBLP Data</v-toolbar-title>
    </v-app-bar>

    <v-content>
      <v-layout >
        <v-text-field
          color="#282828"
          label="Search"
          v-model="searchTerm"
          v-on:keyup.enter="getResults"
        />
        <v-btn color="#282828" v-on:click="getResults">search</v-btn>
      </v-layout>

      <v-container fluid>
        <v-layout >
        <v-row dense>                   
          <v-col>
        <p v-if ="suggestflag">Did you mean <b><i>"{{suggestion}}"</i></b>" ?</p>

          <p v-if ="showHit">Got {{hits}} Hits for <b>"{{suggestion}}"</b></p>
          </v-col>           
          <v-col v-for="(item, i) in items" :key="i" cols="12">

            <v-card dark>
              <div>
                <div align-center>
                  <v-card-title class="headline" >{{item.title}}</v-card-title>
                  <v-card-subtitle >{{item.author}}</v-card-subtitle>
                  <v-card-text>Date Published: {{item.date}}<br/>Journal: {{item.journal}}<br/>Cited by: {{item.citedby}}<br/>Page Rank Score: {{item.pagerank}}<br/>Abstract: {{item.abstract}}</v-card-text>
                  </div>
                </div>
            </v-card>

          </v-col>
           <v-pagination
      v-model="page"
      :length=pagelength
    >
        </v-pagination>
        </v-row>
        </v-layout>
      </v-container>
    </v-content>

    <v-footer app>
      <span>&copy; 2020</span>
    </v-footer>
  </v-app>
</template>

<script>
const axios = require("axios");
export default {
  props: {
    source: String
  },
  data() {
    return{
    drawer: null,
    searchTerm: "",
    items:[],
    hits:0,
    showHit:false,
    suggestflag:false,
    suggestion:"",
    page:1,
    pagelength:0,
    pageitems:[],
    readMoreActivated: false
    }
  },
     methods: {
        activateReadMore: function()
        {        this.readMoreActivated = true;
        },
    getResults: function() {
      var self = this;
      var url = "http://localhost:5000/search?title=" + self.searchTerm;
      // var i;
      self.showProgress = true;
      axios.get(url).then(function(response) {
        console.log(response.data);
        self.items = response.data
        self.hits = response.data[response.data.length-1]['meta']['hits']
        self.pagelength = Math.ceil(self.hits/10)
        self.suggestion=response.data[response.data.length-1]['meta']['suggestion']
        self.suggestflag=response.data[response.data.length-1]['meta']['suggestflag']
        self.showHit=true
        console.log("page:",self.page)
      });
    }
  },
      created () {
      this.$vuetify.theme.dark = true
    },
};
</script>